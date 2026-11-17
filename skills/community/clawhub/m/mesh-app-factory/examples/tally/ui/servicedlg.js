export default {
inject:['service', 'tags'],
data() {return {
    id:0,
    ctrl:{dlg:false,cmt:'',level:0,operable:false},
    dtl:{},
    cmts:[]
}},
emits: ['done'],
props: {
    role:{type:String,required:true},
    tags:{type:Object,required:true},
    alertDlg:{type:Object,required:true},
    confirmDlg:{type:Object,required:true}
},
methods:{
show(id) {
    this.id=id;
    this.cmts=[];
    var url="/api/service/get?id="+id
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var dtl=resp.data;

        var dt=new Date();
        var now=parseInt(dt.getTime()/60000);
        dt.setTime(dtl.createAt*60000);
        dtl.createAt=datetime2str(dt);
        dtl.state_s=this.tags.service.states[dtl.state];
        
        for(var s of dtl.suppliers) {
            if(s.start<=0) {
                s.start_s=this.tags.service.notStart;
            } else {
                dt.setTime(s.start*60000);
                s.start_s=datetime2str(dt);
            }
            if(s.end<=0) {
                s.end_s=this.tags.service.notEnd;
            } else {
                dt.setTime(s.end*60000);
                s.end_s=datetime2str(dt);
            }
            s.ratio=this.service.formatNum(s.ratio*100,1);
            if(s.start==0)s.interval='0';
            else if(s.end>=s.start)s.interval=s.end-s.start;
            else s.interval=now-s.start;
            s.interval+=this.tags.service.unit;
        }

        this.dtl=dtl;
        this.ctrl.dlg=true;
        this.ctrl.operable=this.role=='admin'||dtl.creator==this.service.account;
    })
},
confirm() {
    this.confirmDlg.show(this.tags.cfmServiceAlert, ()=>{
        var url="/api/service/confirm"
        request({method:"PUT",url:url, data:{id:this.id}}, this.service.name).then(resp=>{
            if(resp.code != 0) {
                this.alertDlg.showErr(resp.code, resp.info);
                return;
            }
            this.$emit('done', {act:'cfm'});
            this.ctrl.dlg=false;
        })
    })
},
remove() {
    this.confirmDlg.show(this.tags.rmvServiceAlert, ()=>{
        var url="/api/service/remove?id="+this.id;
        request({method:"DELETE", url:url}, this.service.name).then(resp=>{
            if(resp.code != 0) {
                this.alertDlg.showErr(resp.code, resp.info);
                return;
            }
            this.$emit('done', {act:'rmv'});
            this.ctrl.dlg=false;
        })
    })
},
add_cmt() {
    var url="/api/service/addComment";
    var dta={service:this.id,cmt:this.ctrl.cmt,level:this.ctrl.level};
    request({method:"POST",url:url,data:dta}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.cmt='';
        this.ctrl.level=0;
        this.query_cmts();
    })
},
rmv_cmt(at) {
    var url="/api/service/rmvComment?service="+this.id+"&at="+at;
    request({method:"DELETE",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.query_cmts();
    })
},
query_cmts() {
    var url="/service/comments?service="+this.id;
    request({method:"GET", url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.cmts=[];
            return;
        }
        var dt=new Date();
        this.cmts=resp.data.list.map(c=>{
            dt.setTime(c.at);
            c.at_s=datetime2str(dt);
            return c;
        })
    })
},
expend_cmts() {
    if(this.cmts.length>0) return;
    this.query_cmts();
}
},
template: `
<q-dialog v-model="ctrl.dlg">
<q-card style="min-width:80vw;max-width:90vw">
<q-card-section class="row items-center q-pb-none">
  <div class="text-h6">{{dtl.name}}</div>
  <q-space></q-space>
  <q-btn icon="close" flat round dense v-close-popup></q-btn>
</q-card-section>
<q-card-section>
 <q-markup-table style="width:100%;" flat>
  <tr><td>{{tags.vip.code}}</td><td>{{dtl.code}}</td></tr>
  <tr><td>{{tags.creator}}</td><td>{{dtl.creator}}</td></tr>
  <tr><td>{{tags.createAt}}</td><td>{{dtl.createAt}}</td></tr>
  <tr><td>{{tags.service.state}}</td><td :class="dtl.state=='OK'?'':'text-primary'">{{dtl.state_s}}</td></tr>
  <tr><td>{{tags.service.val}}</td><td>{{dtl.val}}</td></tr>
  <tr><td>{{tags.vip.total}}</td><td>{{dtl.total}}</td></tr>
  <tr><td>{{tags.vip.balance}}</td><td>{{dtl.balance}}</td></tr>
  <tr><td>{{tags.cmt}}</td><td>{{dtl.cmt}}</td></tr>
  <tr v-for="s in dtl.suppliers">
   <td>{{s.account}}</td>
   <td>
    <div class="text-caption">{{s.start_s}}</div>
    <div class="text-caption">{{s.end_s}}</div>
    <div class="text-caption">{{tags.service.useTime}}:{{s.interval}}</div>
    <div class="text-caption">{{tags.brokerage.ratio}}:{{s.ratio}}</div>
   </td>
  </tr>
 </q-markup-table>
 <q-expansion-item dense dense-toggle expand-separator icon="comment"
  :label="tags.service.cmt" @before-show="expend_cmts"
  header-class="text-primary">
 <q-markup-table style="width:100%;" flat>
  <tr v-for="c in cmts">
   <td>
    <div class="text-caption">{{c.cmt}}</div>
    <q-rating v-model="c.level" size="1em" color="orange" readonly></q-rating>
    <div class="text-caption">{{c.at_s}}</div>
   </td>
   <td class="text-right">
    <q-btn color="red" icon="cancel" @click="rmv_cmt(c.at)" flat dense></q-btn>
   </td>
  </tr>
 </q-markup-table>
 <q-input v-model="ctrl.cmt" dense :label="tags.service.cmt">
  <template v-slot:after>
   <q-rating v-model="ctrl.level" color="orange" :max="5"></q-rating>
   <q-btn color="primary" icon="add_circle" @click="add_cmt" flat></q-btn>
  </template>
 </q-input>
 </q-expansion-item>
</q-card-section>

<q-card-actions class="row">
 <div class="col-4 text-left">
  <q-btn flat v-if="ctrl.operable&&dtl.state=='WAIT'" :label="tags.remove" color="red" @click="remove()"></q-btn>
 </div>
 <div class="col-8 text-right q-gutter-sm">
  <q-btn v-if="ctrl.operable&&dtl.state=='END'" dense color="primary"
   :label="tags.confirm" @click="confirm()"></q-btn>
  <q-btn :label="tags.close" flat dense v-close-popup></q-btn>
 </div>
</q-card-actions>
</q-card>
</q-dialog>
`
}