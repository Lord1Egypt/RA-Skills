export default {
inject:['service', 'tags'],
data() {return {
    page:{cur:1, max:0},
    list:[]
}},
created(){
    this.query(1);
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*+this.service.N_PAGE;
    var url="/api/err/list?offset="+offset+"&num="+this.service.N_PAGE
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.list=[];
            return;
        }
        var cols=resp.data.cols;
        var colNum=cols.length;
        var list=[];
        var dt=new Date();
        for(var l of resp.data.errs) {
            var err={};
            for(var i=0;i<colNum;i++) {
                err[cols[i]]=l[i];
            }
            dt.setTime(err.update_time);
            err.at=datetime2str(dt);
            list.push(err);
        }
        this.list=list;
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},

remove(device) {
    var opts={method:"delete",url:"/api/err/remove?code="+encodeURIComponent(device)};
    request(opts, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
        } else {
            this.query(this.page.cur);
        }
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.go_back"></q-btn>
    <q-toolbar-title>{{tags.homeMenus.err.name}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
<q-page-container>
    <q-page class="q-pa-md">
    
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
<q-item v-for="er in list">
 <q-item-section>{{er.device}}</q-item-section>
 <q-item-section>{{er.times}}</q-item-section>
 <q-item-section>{{er.at}}</q-item-section>
 <q-item-section side><q-icon name="delete" color="red" @click="remove(er.device)"></q-icon></q-item-section>
</q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>
`
}