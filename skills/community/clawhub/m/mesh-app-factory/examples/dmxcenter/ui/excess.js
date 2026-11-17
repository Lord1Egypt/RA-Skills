export default {
inject:['service', 'tags'],
data() {return {
    page:{cur:1, max:0},
    list:[],
    alertDlg:null
}},
created(){
    this.query(1);
},
mounted(){//不能在created中赋值，更不能在data中
    this.alertDlg=this.$refs.errDlg;
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*+this.service.N_PAGE;
    var url="/api/err/excess?offset="+offset+"&num="+this.service.N_PAGE
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.list=[];
            return;
        }
        var cols=resp.data.cols;
        var colNum=cols.length;
        var list=[];
        var dt=new Date();
        for(var l of resp.data.list) {
            var req={};
            for(var i=0;i<colNum;i++) {
                req[cols[i]]=l[i];
            }
            dt.setTime(req.day*86400000);
            req.at=date2str(dt);
            list.push(req);
        }
        this.list=list;
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
remove(device,day) {
    var encCode=encodeURIComponent(device);
    var opts={method:"delete",url:"/api/err/removeExcess?code="+encCode+"&day="+day};
    request(opts, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
        } else {
            this.query(this.page.cur);
        }
    })
},
showMsg(code) {
    this.$refs.msgDlg.show(code);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.go_back"></q-btn>
    <q-toolbar-title>{{tags.homeMenus.excess.name}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
<q-page-container>
    <q-page class="q-pa-md">
    
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
<q-item v-for="l in list" @click="showMsg(l.device)" clickable>
 <q-item-section>{{l.device}}</q-item-section>
 <q-item-section>{{l.times}}</q-item-section>
 <q-item-section>{{l.at}}</q-item-section>
 <q-item-section side><q-icon name="delete" color="red" @click="remove(l.device,l.day)"></q-icon></q-item-section>
</q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>
<component-msg-dialog ref="msgDlg" :alertDlg="alertDlg" :tags="tags"
 :serviceName="service.name"></component-msg-dialog>
`
}