export default {
inject:['service', 'tags'],
data() {return {
    id:0,
    ctrl:{dlg:false,rmvDlg:false,operable:false},
    dtl:{}
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
    var url="/api/order/get?id="+id
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var dt=new Date();
        var dtl=resp.data;
        dt.setTime(dtl.createAt*60000);
        dtl.createAt=datetime2str(dt);
        dtl.state_s=this.tags.order.states[dtl.state];
        dtl.refund=dtl.val;
        this.dtl=dtl;
        this.ctrl.dlg=true;
        this.ctrl.operable=this.role=='admin'&&dtl.state=='WAIT';
    })
},
confirm() {
    if(this.role!='admin')return;
    
    this.confirmDlg.show(this.tags.cfmOrderAlert, ()=>{
        var url="/api/order/confirm"
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
    if(this.role!='admin')return;
    var url="/api/order/remove?id="+this.id+"&refund="+this.dtl.refund;
    request({method:"DELETE", url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.$emit('done', {act:'rmv'});
        this.ctrl.rmvDlg=false;
        this.ctrl.dlg=false;
    })
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
  <tr><td>{{tags.order.state}}</td><td :class="dtl.state=='OK'?'':'text-primary'">{{dtl.state_s}}</td></tr>
  <tr><td>{{tags.order.bankAcc}}</td><td>{{dtl.bankAcc}}</td></tr>
  <tr><td>{{tags.order.val}}</td><td>{{dtl.val}}</td></tr>
  <tr><td>{{tags.vip.total}}</td><td>{{dtl.total}}</td></tr>
  <tr><td>{{tags.vip.balance}}</td><td>{{dtl.balance}}</td></tr>
  <tr><td>{{tags.cmt}}</td><td>{{dtl.cmt}}</td></tr>
 </q-markup-table>
</q-card-section>
<q-card-actions class="row">
 <div class="col-4 text-left">
  <q-btn flat v-if="role=='admin'||dtl.state=='WAIT'"
   :label="tags.remove" color="red" @click="ctrl.rmvDlg=true"></q-btn>
 </div>
 <div class="col-8 text-right q-gutter-sm">
  <q-btn v-if="ctrl.operable" dense color="primary" :label="tags.confirm" @click="confirm()"></q-btn>
  <q-btn :label="tags.close" flat dense v-close-popup></q-btn>
 </div>
</q-card-actions>
</q-card>
</q-dialog>

<q-dialog v-model="ctrl.rmvDlg">
 <q-card style="min-width:40vw;">
    <q-card-section>
     <div class="text-h6">{{tags.alert}}</div>
    </q-card-section>
    <q-separator></q-separator>
    <q-card-section class="q-pt-none">{{tags.rmvOrderAlert}}</q-card-section>
    <q-card-section class="q-pt-none" v-if="dtl.state=='OK'">
     <q-input v-model="dtl.refund" :label="tags.order.refund" dense></q-input>
    </q-card-section>
    <q-card-actions align="right" class="q-pr-md">
     <q-btn :label="tags.ok" color="primary" @click="remove"></q-btn>
     <q-btn flat :label="tags.cancel" color="primary" v-close-popup></q-btn>
    </q-card-actions>
 </q-card>
</q-dialog>
`
}